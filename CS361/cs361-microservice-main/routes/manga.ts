import express from "express";
const router = express.Router();
import getMangaByTitle from "../controllers/getController";
import { JIKAN_MANGA_SEARCH_ENDPOINT } from "../utils/constants";

router.route("/").get(getMangaByTitle(JIKAN_MANGA_SEARCH_ENDPOINT));

export default router;
