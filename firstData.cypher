CREATE (u1:User {id: "u1", name: "José Sanchez"})
CREATE (u2:User {id: "u2", name: "Jose Abril"})
CREATE (u3:User {id: "u3", name: "Josué García"})

CREATE (m1:Movie {id: "m1", title: "Inception"})
CREATE (m2:Movie {id: "m2", title: "Interstellar"})

CREATE (a1:Actor {name:"Leonardo DiCaprio", role: "Protagonista"})

CREATE (scifi:Genre {name: "Sci-Fi"})
CREATE (nolan:Director {name: "Christopher Nolan", country: "UK"})

CREATE (m1)-[:HAS_GENRE] -> (scifi)
CREATE (m2)-[:HAS_GENRE] -> (scifi)
CREATE (m1)-[:DIRECTED_BY] -> (nolan)
CREATE (m2)-[:DIRECTED_BY] -> (nolan)
CREATE (m1)-[:HAS_ACTOR] -> (a1)
