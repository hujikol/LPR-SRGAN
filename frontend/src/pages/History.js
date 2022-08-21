// This file is showing history of all LPR result with their
// coresponding Base detected image, SRGAN result, and OCR result

import React from "react";
import { Outlet } from "react-router-dom";

function History() {
  return (
    <>
      <h1> this is the history page </h1>
      <Outlet />
    </>
  );
}

export default History;
