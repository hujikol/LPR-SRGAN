import React from "react";
import { NavLink } from "react-router-dom";

function Footer() {
  return (
    <footer class='mt-auto p-4 bg-white shadow-inner md:flex md:items-center md:justify-between md:p-6'>
      <span class='text-sm text-gray-500 sm:text-center'>
        © 2022{" "}
        <NavLink className='hover:underline' to='/'>
          Nicholas Nanda Sulaksana
        </NavLink>
      </span>
      <ul class='flex flex-wrap items-center mt-3 text-sm text-gray-500 sm:mt-0'>
        <NavLink className='mr-4 hover:underline md:mr-6' to='/'>
          Uji Coba
        </NavLink>
        <NavLink className='mr-4 hover:underline md:mr-6' to='/riwayat'>
          Riwayat
        </NavLink>
        <NavLink className='mr-4 hover:underline md:mr-6' to='/tentang'>
          Tentang
        </NavLink>
      </ul>
    </footer>
  );
}

export default Footer;
