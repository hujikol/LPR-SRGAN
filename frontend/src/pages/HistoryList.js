import React from "react";
import { Link } from "react-router-dom";

function HistoryList() {
  return (
    <div className='container mx-auto mt-8'>
      <div className='flex flex-col items-center'>
        <Link to='/history/1'>
          <h1> this is HistoryList number 1</h1>
        </Link>
        <Link to='/history/2'>
          <h1> this is HistoryList number 2</h1>
        </Link>
      </div>
    </div>
  );
}

export default HistoryList;
