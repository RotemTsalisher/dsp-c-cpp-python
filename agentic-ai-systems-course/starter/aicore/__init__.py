"""Shared primitives for the bench-ai system.

`aicore` is nobody's module and everybody's dependency, which makes it the one
place where a careless change affects every agent. Treat it as a published
interface: changes here go through the contract-change protocol (Module 07),
not through a module agent.
"""
