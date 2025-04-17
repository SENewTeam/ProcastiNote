import React, { useState } from 'react';

const Author = () => {
  if (!localStorage.getItem("token")) {
    window.location.href = "/login";
  }
  return (
    <>
    <h1>Author Page</h1>
    </>
  );
};

export default Author