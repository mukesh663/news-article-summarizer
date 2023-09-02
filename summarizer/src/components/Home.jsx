import React, { useState } from "react";
import Navbar from "./Navbar";
import Footer from "./Footer";

function Home() {
  const [text, setText] = useState("");
  const [responseData, setResponseData] = useState(null);

  const handleUpload = async e => {
    if(!text) {
      alert("Please input a text"); 
      return;
    }
    e.preventDefault();
    const formData = new FormData();
    formData.append("text", text);
    const url = `http://127.0.0.1:8000/result/${encodeURIComponent(text)}`; // Include the text parameter in the URL

    await fetch(url, {
      method: "POST",
      body: formData
    }).then((response) => response.json())
    .then((data) => 
      setResponseData(data)
    )
    .catch((error) => console.log(error));

  };

  return (

    <div className="flex flex-col h-screen justify-between">
    <Navbar />
    <div className="items-center mt-10 justify-center text-center">
      <p className="text-gray-700 text-2xl leading-loose" >
        Welcome to Summarizer! A web app that helps you summarize your news articles with NLP and EM techniques.
      </p>
      <p className="text-2xl font-medium leading-loose">
        Summarize your news articles in seconds!
      </p>

    </div>

    <div className="mt-2">
        <div className="flex items-center justify-center">
          <textarea id="message" rows="5" class="block p-2.5 w-1/2 text-lg text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-stone-50 dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Input your news articles..." onChange={(e) => setText(e.target.value)}></textarea>
        </div> 
       
        <div className="flex m-10 items-center justify-center">
        <button className="flex justify-center rounded-md bg-indigo-600 px-5 py-2.5 text-lg font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" onClick={handleUpload}>Summarize</button>
        </div>

        {responseData && (
          <>
          <div className="flex m-0 justify-center">
            <div
              id="message"
              className="block p-2.5 w-1/2 text-lg  bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-stone-50 dark:focus:ring-blue-500 dark:focus:border-blue-500"
              contentEditable={false}
            >
              {responseData.result}
            </div>
          </div>
          
          <div className="flex m-5 justify-center">
            <div className="w-1/2 ">
            <p className="mb-2 text-lg">Positivity: {responseData.pos_sentiment}</p>
            <p className="mb-2 text-lg">Negativity: {responseData.neg_sentiment}</p>
            <p className="text-lg">Neutrality: {responseData.neu_sentiment}</p>
            </div>
          </div>
          </>
        )}
    </div>
    <Footer />
    </div>
  )
}

export default Home