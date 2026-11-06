def coin_change(coins,amount):
    dp=[10**9]*(amount+1); dp[0]=0
    for a in range(1,amount+1):
        for c in coins:
            if c<=a: dp[a]=min(dp[a],dp[a-c]+1)
    return dp[amount]
