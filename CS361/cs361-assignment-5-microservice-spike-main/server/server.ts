import express, { NextFunction, Request, Response } from "express";

const app = express();
const PORT = 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});

app.post("/", (req: Request, res: Response) => {
  console.log(`Received HTTP ${req.method} request`);
  console.log(req.body);
  res.json(200);
});

app.all("*", (_req: Request, _res: Response, next: NextFunction) => {
  next(Error("resource not found"));
});

app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
  res.send(err.message);
});
