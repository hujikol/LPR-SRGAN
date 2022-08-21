// This file is showing history of all LPR result with their
// coresponding Base detected image, SRGAN result, and OCR result

import React from "react";
import { Outlet } from "react-router-dom";

function History() {
  return (
    <div className='container mx-auto mt-16'>
      <div className='flex flex-col'>
        <h1 className='text-2xl font-bold self-center'>Halaman Riwayat</h1>
        <Outlet />
      </div>
    </div>
  );
}

export default History;
