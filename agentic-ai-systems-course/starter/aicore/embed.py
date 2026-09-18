"""Embedders, offline and real.

Two offline implementations are provided on purpose, and they fail in opposite
ways. Running the course exercises against both is how you develop an intuition
for what semantic search does and does not buy you (Module 10).

    HashEmbedder   bag of words. NOT semantic. "clipping" and "saturation" are
                   orthogonal. Exists to make the limitation concrete.
    TfidfEmbedder  character n-grams + idf. Lexical, robust to identifiers and
                   typos, still not semantic. Strong on `agc_attack_ms`, weak on
                   synonymy - which is exactly the hybrid-search argument.
"""
from __future__ import annotations

import hashlib
import math
import os
import re
from collections import Counter
from pathlib import Path
from typing import Protocol

import numpy as np


class Embedder(Protocol):
    dim: int
    name: str

    def embed(self, texts: list[str], *, is_query: bool = False) -> np.ndarray: ...


def _bucket(token: str, dim: int) -> int:
    """Stable across processes.

    NOT `hash()`: Python salts string hashing per interpreter run, so an index
    built today would not match a query tomorrow. That bug is invisible in a
    single process and catastrophic after a restart.
    """
    return int.from_bytes(hashlib.blake2b(token.encode(), digest_size=8).digest(), "big") % dim


def _l2(matrix: np.ndarray) -> np.ndarray:
    return matrix / np.maximum(np.linalg.norm(matrix, axis=1, keepdims=True), 1e-9)


class HashEmbedder:
    """Deterministic, dependency-free, deliberately not semantic."""

    name = "hash-v1"

    def __init__(self, dim: int = 256) -> None:
        self.dim = dim

    def embed(self, texts: list[str], *, is_query: bool = False) -> np.ndarray:
        out = np.zeros((len(texts), self.dim), dtype=np.float32)
        for row, text in enumerate(texts):
            for word in re.findall(r"\w+", text.lower()):
                out[row, _bucket(word, self.dim)] += 1.0
        return _l2(out)


class TfidfEmbedder:
    """Character n-gram TF-IDF projected into a fixed dimension."""

    def __init__(self, dim: int = 512, n: int = 4) -> None:
        self.dim = dim
        self.n = n
        self.name = f"tfidf-char{n}-d{dim}-v1"
        self.idf: dict[int, float] = {}
        self._fitted = False

    def _grams(self, text: str) -> list[int]:
        normalized = " " + re.sub(r"\s+", " ", text.lower()) + " "
        return [_bucket(normalized[i : i + self.n], self.dim) for i in range(len(normalized) - self.n + 1)]

    def fit(self, texts: list[str]) -> "TfidfEmbedder":
        document_freq: Counter[int] = Counter()
        for text in texts:
            document_freq.update(set(self._grams(text)))
        total = max(len(texts), 1)
        self.idf = {gram: math.log((total + 1) / (freq + 1)) + 1.0 for gram, freq in document_freq.items()}
        self._fitted = True
        return self

    def embed(self, texts: list[str], *, is_query: bool = False) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("TfidfEmbedder.fit(corpus) must be called before embed()")
        out = np.zeros((len(texts), self.dim), dtype=np.float32)
        for row, text in enumerate(texts):
            for gram, count in Counter(self._grams(text)).items():
                out[row, gram] += (1.0 + math.log(count)) * self.idf.get(gram, 1.0)
        return _l2(out)


class CachedEmbedder:
    """Cache by content hash.

    The key includes the embedder NAME. Without it, switching models returns
    vectors from the old model - document vectors from one geometry, query
    vectors from another, high cosine scores, meaningless ranking, no error.
    """

    def __init__(self, inner: Embedder, path: Path) -> None:
        self.inner = inner
        self.path = Path(path)
        self.dim = inner.dim
        self.name = inner.name
        self._cache: dict[str, np.ndarray] = {}
        self.hits = 0
        self.misses = 0
        if self.path.exists():
            with np.load(self.path) as data:
                self._cache = {key: data[key] for key in data.files}

    def _key(self, text: str, is_query: bool) -> str:
        return hashlib.sha256(f"{self.name}|{int(is_query)}|{text}".encode()).hexdigest()

    def embed(self, texts: list[str], *, is_query: bool = False) -> np.ndarray:
        keys = [self._key(t, is_query) for t in texts]
        missing = [(k, t) for k, t in zip(keys, texts) if k not in self._cache]
        self.hits += len(texts) - len(missing)
        self.misses += len(missing)
        if missing:
            fresh = self.inner.embed([t for _, t in missing], is_query=is_query)
            for (key, _), vector in zip(missing, fresh):
                self._cache[key] = vector
            self.path.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(self.path, **self._cache)
        return np.stack([self._cache[k] for k in keys])


class ProviderEmbedder:
    """Adapter for a hosted embedding model.

    `query_prefix` / `doc_prefix` matter: several popular models are trained with
    asymmetric prefixes ("query: " / "passage: "). Omitting them costs real
    accuracy and produces no error. Check the model card.
    """

    def __init__(self, client, model: str, dim: int, batch: int = 96,
                 query_prefix: str = "", doc_prefix: str = "") -> None:
        self.client = client
        self.model = model
        self.dim = dim
        self.batch = batch
        self.name = f"{model}-d{dim}"
        self.query_prefix = query_prefix
        self.doc_prefix = doc_prefix

    def embed(self, texts: list[str], *, is_query: bool = False) -> np.ndarray:
        prefix = self.query_prefix if is_query else self.doc_prefix
        payload = [prefix + t for t in texts]
        vectors: list[list[float]] = []
        for start in range(0, len(payload), self.batch):
            response = self.client.embeddings.create(model=self.model, input=payload[start : start + self.batch])
            vectors.extend(item.embedding for item in response.data)
        return _l2(np.asarray(vectors, dtype=np.float32))


def get_embedder(corpus_texts: list[str] | None = None) -> Embedder:
    """Factory. Offline unless BENCH_AI_EMBEDDER says otherwise."""
    kind = os.environ.get("BENCH_AI_EMBEDDER", "tfidf")
    if kind == "hash":
        return HashEmbedder()
    if kind == "openai":
        from openai import OpenAI

        return ProviderEmbedder(OpenAI(), model=os.environ.get("BENCH_AI_EMBED_MODEL", "text-embedding-3-small"), dim=1536)
    embedder = TfidfEmbedder()
    if corpus_texts:
        embedder.fit(corpus_texts)
    return embedder
