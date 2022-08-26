import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function HistoryList() {
  const [historyList, setHistoryList] = useState([]);
  useEffect(() => {
    fetch("http://localhost:8000/image")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setHistoryList(data);
      })
      .catch((e) => {
        console.log(e.message);
      });
  }, []);

  const date = "18:35:20 12/09/2022";

  return (
    <div className='container mx-auto mt-8'>
      <div className='flex flex-wrap xl:ml-24 lg:mx-2 md:mx-12 md:justify-start sm:justify-center'>
        {historyList.map((data) => {
          return (
            <div className='max-w-xs bg-white rounded-lg border border-gray-200 shadow-md m-2'>
              <Link to='/riwayat/2'>
                <div className='max-h-52 overflow-hidden'>
                  <img
                    className='rounded-t-lg'
                    src={require("./../testAssets/3abf17e4fd8417d7.png")}
                    alt=''
                  />
                </div>
              </Link>
              <div className='p-5'>
                <Link to='/riwayat/2'>
                  <h5
                    className='mb-2 text-2xl font-bold tracking-tight text-gray-700'
                    key={data.id}
                  >
                    {console.log("dataId:", data.id)}
                    {console.log("dataImg:", data.img_path)}B 1234 CXS{" "}
                    {data.img_path}
                    <span className='mb-3 text-xl font-normal text-gray-400'>
                      , 2 lainnya..
                    </span>
                  </h5>
                </Link>
                <p className='mb-3 font-normal text-gray-400'>
                  Diproses Pada: <br />
                  {date}
                </p>
                <Link
                  to='/riwayat/2'
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
