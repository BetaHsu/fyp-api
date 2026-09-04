# Re-collect — API

Flask and MongoDB backend for [Re-collect](https://github.com/BetaHsu/fyp): *a social writing platform where another person's work is only partially visible until you rewrite it, and rewriting is what makes it more visible to everyone.*

Final year project, City University of Hong Kong, 2023. See the [frontend repo](https://github.com/BetaHsu/fyp) for the rest.

## What it handles

Every visibility rule is enforced here, never in the client:

- Paragraph storage, each paragraph tracking its own revealed and hidden intervals
- Reveal-score calculation across a work, and time-based decay of sections revealed earlier
- The rewrite transaction: publishing a rewrite reveals the sections its author selected, grants that author full access to the original, and appends their contribution to the original's shared piece
- Resolving what each viewer is allowed to receive, so hidden text never leaves the server
- Users, sign in and sign up

## Structure

```
app.py                        Flask app, ObjectId JSON encoding
controllers/v1                route handlers
services/database_service.py  all MongoDB access
```

The connection string is read from the `MONGODB_URI` environment variable. No credentials are stored in this repository.

## Status

Built in 2023, no longer maintained. Public as a record of the project.

## License

© 2023 Beta HSU Yun Chu. All rights reserved. The code is readable here for reference. The system design and the concept behind it are not licensed for reuse, and I am still developing them.
