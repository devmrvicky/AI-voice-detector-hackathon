import express from "express";
import { getUrl } from "../controllers/url.controller";

const router = express.Router();

router.post("/url", getUrl);

export default router;
