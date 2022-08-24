// upload image in jpg,jpeg,png, or a video,
// or even start capturing stream from cctv
// then showing single result
// or all detected plates if that is video input

import React from "react";

import DropBox from "./../components/DropBox";

function Home() {
  return (
    <div className='container mx-auto mt-16 mb-24'>
      {/* tittle div */}
      <div className='flex justify-center'>
        <h1 className='text-2xl font-bold text-center'>
          Uji Coba Pengenalan Karakter
          <br />
          Plat Nomor Kendaraan Roda Empat
        </h1>
      </div>
      {/* end of tittle div */}
      {/* drop zone */}
      <DropBox />
      {/* drop zone */}
    </div>
  );
}

export default Home;
