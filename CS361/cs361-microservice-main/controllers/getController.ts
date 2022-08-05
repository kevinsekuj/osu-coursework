import axios, { AxiosResponse } from "axios";
import { NextFunction, Request, Response } from "express";
import HTTPError from "../utils/error";

const getMediaByTitle = (endpoint: string) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const { title } = req.query;
    if (typeof title !== "string" || !title) {
      return next(
        new HTTPError("Query parameter 'title' must be of type string.")
      );
    }

    try {
      const response: AxiosResponse = await axios.get(`${endpoint}?q=${title}`);
      if (response.status !== 200)
        throw new HTTPError("Jikan API GET Request failed");

      res.json(response.data);
    } catch (e) {
      let errorMessage = "GET request failed";
      if (e instanceof Error) errorMessage = e.message;

      return next(new HTTPError(errorMessage));
    }
  };
};

export default getMediaByTitle;
