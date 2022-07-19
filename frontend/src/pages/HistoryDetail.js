import React, { useEffect } from "react";
import { useParams } from "react-router";

function HistoryDetail() {
  let { postSlug } = useParams();

  useEffect(() => {}, [postSlug]);

  return (
    <>
      <h1>this is in the detailed post {postSlug}</h1>
    </>
  );
}

export default HistoryDetail;
