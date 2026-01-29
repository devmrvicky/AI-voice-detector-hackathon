import express from "express";
import dotenv from "dotenv";
import { rateLimit } from "express-rate-limit";
import { authorizeAPIKey } from "./middlewares/authorization.middleware";
import URLRouter from "./routes/url.route";

dotenv.config({});

const app = express();

const port = process.env.PORT || 9000;

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  limit: 100,
});

app.use(limiter);
app.use(express.json());
app.use(authorizeAPIKey);

app.get("/test", (req, res) => {
  res.send({ server_testing: "ok" });
});

app.use("/api", URLRouter);

app.listen(port, () => {
  console.log(`🚀server running on port : ${port}`);
});
