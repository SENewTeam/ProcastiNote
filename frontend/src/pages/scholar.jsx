import React, { useState } from 'react';

const Scholar = () => {
  if (!localStorage.getItem("token")) {
    window.location.href = "/login";
  }
  return (
    <>
    <h1>Scholar Page</h1>
    </>
  );
};

export default Scholar