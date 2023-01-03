import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import ScaleLoader from "react-spinners/ScaleLoader";

function HistoryList() {
  const [historyList, setHistoryList] = useState([]);
  console.log("ini di history list");
  const client = axios.create({
    baseURL: "http://localhost:8000",
  });

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const fetchHistory = async () => {
    try {
      const apiRes = await client.get(`/get-history/all`);
      console.log("res", apiRes);
      if (apiRes) setHistoryList(apiRes.data.historyData);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchHistory();
    console.log("historylis", historyList);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className='container mx-auto mt-8'>
      {historyList === 0 && (
        <div className='flex flex-col items-center'>
          <img
            className='mt-4 object-contain h-48 w-96'
            src={require("./../assets/no-data.jpg")}
            alt='Author_Profile_Picture'
          />
          <p className='text-normal text-center text-gray-400'>
            Maaf belum ada data tersimpan, <br />
            buat satu{" "}
            <Link className='underline italic' to='/'>
              disini
            </Link>
          </p>
        </div>
      )}
      {historyList.length === 0 && (
        <div className='flex flex-col items-center mt-16'>
          <ScaleLoader
            color='#3F83F8'
            height={30}
            speedMultiplier={0.8}
            width={8}
          />
        </div>
      )}
      <div className='flex flex-wrap xl:ml-24 lg:mx-2 md:mx-12 md:justify-start sm:justify-center'>
        {historyList !== 0 &&
          historyList.map((data) => {
            return (
              <div className='max-w-xs bg-white rounded-lg border border-gray-200 shadow-md m-2'>
                <Link to={`${data.historyId}`}>
                  <div className='max-h-52 overflow-hidden'>
                    <img
                      className='rounded-t-lg'
                      src={`data:image/jpeg;base64,${data.inputImg_byte}`}
                      alt=''
                    />
                  </div>
                </Link>
                <div className='p-5'>
                  <Link to={`${data.historyId}`}>
                    <h5
                      className='mb-2 text-2xl font-bold tracking-tight text-gray-700'
                      key={data.historyId}
                    >
                      Pengenalan Ke - {data.historyId}
                    </h5>
                  </Link>

                  <p className='font-normal text-gray-400'>
                    {data.bboxCount} Plat Terdeteksi
                  </p>
                  <p className='mb-3 font-normal text-gray-400'>
                    Diproses Pada: <br />
                    {data.dateTime}
                  </p>
                  <Link
                    to={`${data.historyId}`}
                    className='inline-flex items-center py-2 px-3 text-sm font-medium text-center text-white bg-blue-500 rounded-lg hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300'
                  >
                    Detail
                    <svg
                      aria-hidden='true'
                      className='ml-2 -mr-1 w-4 h-4'
                      fill='currentColor'
                      viewBox='0 0 20 20'
                      xmlns='http://www.w3.org/2000/svg'
                    >
                      <path
                        fillRule='evenodd'
                        d='M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z'
                        clipRule='evenodd'
                      ></path>
                    </svg>
                  </Link>
                </div>
              </div>
            );
          })}
      </div>
    </div>
  );
}

export default HistoryList;
