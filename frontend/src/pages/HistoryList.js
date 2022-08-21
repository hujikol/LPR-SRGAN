import React from "react";
import { Link } from "react-router-dom";

function HistoryList() {
  return (
    <>
      <Link to='/History/1'>
        <h1> this is HistoryList number 1</h1>
      </Link>
      <Link to='/History/2'>
        <h1> this is HistoryList number 2</h1>
      </Link>
    </>
  );
}

export default HistoryList;
