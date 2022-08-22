import React from "react";

function About() {
  return (
    <div className='container mx-auto mt-16'>
      <div className='flex flex-col items-center'>
        <h1 className='text-2xl text-center font-bold'>
          Halo saya, <br /> Nicholas Nanda
        </h1>
        <img
          className='mt-4 rounded-full max-h-64'
          src={require("./../assets/profile.jpg")}
          alt='Author_Profile_Picture'
        />
        <p className='mt-8 mx-16 max-w-2xl text-justify'>
          &emsp;&emsp;Aplikasi ini dibuat untuk memenuhi Tugas Akhir dalam
          menempuh gelar S1 di Universitas Pembangunan Nasional "Veteran"
          Yogyakarta. Tugas Akhir saya memiliki judul yaitu{" "}
          <b>
            {" "}
            "Implementasi{" "}
            <em>Super Resolution Generative Adversarial Network</em> untuk
            Peningkatan Akurasi pada Pengenalan Plat Nomor Kendaraan Roda Empat"
          </b>
          .
        </p>
      </div>
    </div>
  );
}

export default About;
