# Subdocument Array Mutation

This project provides a library that allows updating a subdocument array in a DB.

Sample Input/Output:
### Input:
```json 
{ "posts": [{"_id": 2, "value": "too"}] }
```

### Output:
```json
{ "$update": {"posts.0.value": "too"} }
```

### Input
```json
{ "posts": [{"_id": 3, "mentions": [ {"_id": 5, "text": "pear"}]}] }
```

### Output:
```json
{ "$update": {"posts.1.mentions.0.text": "pear"}}
```
