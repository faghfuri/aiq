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

## Schema

The Objects that are created in this DB have the following schema:

```golang
type Creator struct {
	ID    int64  `json:"_id"`
	Name  string `json:"name"`
	Posts []Post `json:"posts"`
}

type Post struct {
	ID       int64     `json:"_id"`
	Value    string    `json:"value"`
	Mnetions []Mention `json:"mentions"`
}

type Mention struct {
	ID   int64  `json:"_id"`
	Text string `json:"text"`
}

```

  
  
