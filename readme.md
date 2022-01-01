TODO:
1. migrate nodes in the graph to store just Token:int instead of Future.
2. migrate edges in the graph to store just OpToken:int instead of Operation.
3. support materialized variables, remove Future wrapping when not needed.
4. generalize the underlying graph engine to not include things like performanceSpecs and OperationProperties, 
instead wrap it with it.