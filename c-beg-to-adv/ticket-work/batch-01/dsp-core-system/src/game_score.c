#include "dsp/game_score.h"

int game_score_on_hit(int const score, int const picked_bin, int const target_bin)
{
    if (picked_bin == target_bin) {
        return score;
    }
    return score;
}
