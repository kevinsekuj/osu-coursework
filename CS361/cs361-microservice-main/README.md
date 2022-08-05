# Jikan Anime/Manga microservice

## Usage

First time

    npm install

Every time

     npm start

The microservice will now be accessible at http://localhost:3000 by default.

## Requesting/Receiving Data

This microservice leverages the Jikan API to return data about a user-supplied anime/manga. Queries are made with the query string `?title=<string>`. Data is received as JSON objects with HTTP status code 200 for successful responses. Failed requests will return HTTP codes 400/404.

### Endpoints

`/anime`

`/manga`

### Example Request (JavaScript Fetch API)

    fetch('http://localhost:3000/anime?title=shingeki-no-kyojin)
      .then(response => response.json())
      .then(data => console.log(data));

### Example Response:

    data:
    [
        {
            mal_id:  16498,
            title:  "Shingeki no Kyojin",
            title_english:  "Attack on Titan",
            title_japanese:  "進撃の巨人",

    		...
    	}
    ]

## UML Sequence Diagram

```mermaid
sequenceDiagram
Client->>Microservice: Client makes GET request to endpoint
Note over Client: /anime
Note over Client: /manga
Note over Client: query param: title

Microservice->> Jikan API: Microservice requests external Jikan API
Note over Microservice: query param: q

alt  Success
Jikan API->>Microservice: Request succeeded
Note left of Jikan API: 200 OK
else Error
Jikan API->>Microservice: Request failed
Note left of Jikan API:  400 Bad request <br> 404 Resource Not Found <br> 405 Method Not Allowed <br> 429 Too Many Requests <br> 500 Internal Server Error <br> 503 Service Unavailable
end
alt  Success

Microservice ->> Client: Request succeeded: 200
Note left of Microservice: 200 OK
else Error
Microservice->>Client: Request failed
Note left of Microservice:  400 Bad Request <br> 404 Resource Not Found
end
```
