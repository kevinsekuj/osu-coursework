if (process.env.NODE_ENV !== "production") {
  require("dotenv").config();
}

import express, { Request, Response, NextFunction } from "express";
import cors from "cors";
const app = express();

const PORT = process.env.PORT || 3000;

import anime from "./routes/anime";
import manga from "./routes/manga";
import HTTPError from "./utils/error";

app.use(cors());
app.use(express.json());

app.use("/anime", anime);
app.use("/manga", manga);

app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});

app.get("/anime", (_req: Request, res: Response) => {
  res.redirect("anime");
});

app.get("/manga", (_req: Request, res: Response) => {
  res.redirect("manga");
});

app.all("*", (_req: Request, _res: Response, next: NextFunction) => {
  next(new HTTPError("Resource not found", 404));
});

app.use((err: HTTPError, _req: Request, res: Response, _next: NextFunction) => {
  res.status(err.status).json({ error: err.message, status: err.status });
});
