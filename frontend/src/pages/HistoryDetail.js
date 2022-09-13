import React, { useState, useEffect } from "react";
import { useParams } from "react-router";
import axios from "axios";
import ScaleLoader from "react-spinners/ScaleLoader";

function HistoryDetail() {
  const { postSlug } = useParams();
  const [historyData, setHistoryData] = useState([]);

  const client = axios.create({
    baseURL: "http://localhost:8000",
  });

  const fetchHistoryData = async () => {
    try {
      const apiRes = await client.post(`/get-history/${postSlug}`);
      console.log("res", apiRes);
      if (apiRes) setHistoryData(apiRes.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchHistoryData();
    console.log("historyData", historyData);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className='container mx-auto mt-2'>
      <div className='flex flex-col items-center'>
        <div>
          <h1 className='text-xl font-bold text-center'>
            Detail Pengenalan Ke - {postSlug}
          </h1>
        </div>

        {historyData.length === 0 && (
          <div className='flex flex-col items-center mt-16'>
            <ScaleLoader
              color='#3F83F8'
              height={30}
              speedMultiplier={0.8}
              width={8}
            />
          </div>
        )}

        {/* Main Image Start*/}
        <div className='max-w-2xl mx-auto mt-2 rounded-lg border'>
          <img
            className='rounded-t-lg'
            src={`data:image/jpeg;base64,${historyData.yolo_img_byte}`}
            alt=''
          />
        </div>
        {/* Main Image End*/}
        <div className='mt-2'>
          <span className='text-center'>
            Average Confidence YOLOv4:{" "}
            <b>{(historyData.yolo_confidence * 100).toFixed(2)}%</b>
          </span>
        </div>

        {historyData.cns_data?.map((data) => {
          return (
            <div className='flex flex-row justify-between mx-auto mt-12'>
              <div>
                {/*Cropped Card Start */}
                <div className='max-w-xs mr-12 bg-white rounded-lg border border-gray-200 shadow-md'>
                  <div className='max-h-42 overflow-hidden'>
                    <img
                      className='object-contain h-42 w-full rounded-t-lg'
                      // change Image here
                      src={`data:image/jpeg;base64,${data.crop_img_byte}`}
                      alt=''
                    />
                  </div>
                  <div className='p-5'>
                    <h3 className='mb-2 text-xl font-bold tracking-tight text-gray-700'>
                      Hasil <em>Cropping</em> Plat Nomor
                    </h3>
                    <p className='mb-3 text-gray-700'>
                      <b>Karakter Terdeteksi Tanpa Otsu's</b>
                      <br />
                      {data.crop_wo_text}
                    </p>
                    <p className='mb-3 text-gray-700'>
                      <b>Karakter Terdeteksi dg Otsu's</b>
                      <br />
                      {data.crop_text}
                    </p>
                    <p className='mb-3 text-gray-700'>
                      <b>Ukuran File</b>
                      <br />
                      {parseFloat(data.crop_img_size).toFixed(2)} KB
                    </p>
                  </div>
                </div>
                {/* Cropped Ends */}
              </div>
              <div>
                {/*SRGAN Card Start */}
                <div className='max-w-xs bg-white rounded-lg border border-gray-200 shadow-md'>
                  <div className='max-h-52 overflow-hidden'>
                    <img
                      className='w-full rounded-t-lg'
                      // change Image here
                      src={`data:image/jpeg;base64,${data.super_img_byte}`}
                      alt=''
                    />
                  </div>

                  <div className='p-5'>
                    <h3 className='mb-2 text-xl font-bold tracking-tight text-gray-700'>
                      Hasil <em>Super-Resolution</em>
                    </h3>

                    <p className='mb-3 text-gray-700'>
                      <b>Karakter Terdeteksi Tanpa Otsu's</b>
                      <br />
                      {data.super_wo_text}
                    </p>
                    <p className='mb-3 text-gray-700'>
                      <b>Karakter Terdeteksi dg Otsu's</b>
                      <br />
                      {data.super_text}
                    </p>
                    <p className='mb-3 text-gray-700'>
                      <b>Ukuran File</b>
                      <br />
                      {parseFloat(data.super_img_size).toFixed(2)} KB
                    </p>
                  </div>
                </div>
                {/* SRGAN Ends */}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default HistoryDetail;
