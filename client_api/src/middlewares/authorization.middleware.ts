import { Request, Response, NextFunction } from "express";

export const authorizeAPIKey = async (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  try {
    const api_key = req.headers["x-api-key"];
    if (!api_key) {
      console.log("❌ api key is missing");
      res.status(404).send("api key is missing");
      return;
    }
    if (api_key !== process.env.API_KEY) {
      console.log("Authorization failled.");
      res.status(401).send("Authorization failled.");
      return;
    }
    console.log(api_key);
    next();
  } catch (error) {
    res.status(500).send("server error");
  }
};
