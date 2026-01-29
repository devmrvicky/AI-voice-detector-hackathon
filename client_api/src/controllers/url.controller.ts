import axios from "axios";
import { Request, Response } from "express";
import fs from "node:fs/promises";
import { Buffer } from "node:buffer";

export const getUrl = async (req: Request, res: Response) => {
  try {
    const { audio_url, language } = req.body;
    if (!audio_url || !language) {
      res.status(400).send("audio_url and language are required");
      return;
    }
    // check audio url validation
    const parsedUrl = new URL(audio_url);
    if (
      "http:".includes(parsedUrl.protocol) === false &&
      "https:".includes(parsedUrl.protocol) === false
    ) {
      res.status(400).send("Invalid audio_url");
      return;
    }
    // download audio from url and process it
    const response = await axios.get(audio_url, {
      responseType: "arraybuffer",
    });
    const audioData = response.data as ArrayBuffer;
    console.log(`Audio data length: ${audioData.byteLength} bytes`);
    console.log(audioData);
    const filePath = "./src/temp/audio.mp3";
    await fs.writeFile(filePath, Buffer.from(audioData));
    res.status(200).send({ message: "Audio processed successfully" });
  } catch (error) {
    res.status(500).send("server error");
  }
};
