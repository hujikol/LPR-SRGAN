import React, { useEffect } from "react";
import { useParams } from "react-router";

function HistoryDetail() {
  let { postSlug } = useParams();

  useEffect(() => {}, [postSlug]);

  return (
    <>
      <h1>Riwayat Pengenalan Karakter {postSlug}</h1>
    </>
  );
}

export default HistoryDetail;
