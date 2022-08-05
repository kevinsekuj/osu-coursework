import express from "express";
const router = express.Router();
import getMediaByTitle from "../controllers/getController";
import { JIKAN_ANIME_SEARCH_ENDPOINT } from "../utils/constants";

router.route("/").get(getMediaByTitle(JIKAN_ANIME_SEARCH_ENDPOINT));

export default router;
