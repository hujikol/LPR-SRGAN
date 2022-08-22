import React from "react";
import { NavLink, useLocation } from "react-router-dom";

function Navbar() {
  const pathName = useLocation().pathname;

  return (
    <nav className='container mx-auto mt-8'>
      <div className='flex flex-row justify-center'>
        <div className='px-4'>
          <NavLink className={`${pathName === "/" ? "font-bold" : ""}`} to=''>
            Uji Coba
          </NavLink>
        </div>

        <div className='px-4'>
          <NavLink
            className={`${pathName === "/riwayat" ? "font-bold" : ""}`}
            to='/riwayat'
          >
            Riwayat
          </NavLink>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
