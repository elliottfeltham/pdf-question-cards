import React from "react";
import Header from "./components/Header";
import Button from "./components/Button";
import "./styles/App.css";

const fileInputRef = React.createRef<HTMLInputElement>();

const handleUploadButton = () => {
	fileInputRef.current?.click();
};

const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
	const file = event.target.files?.[0];
	if (!file) {
		console.log("No file selected");
		return;
	}
	console.log("Selected file:", file);
	// Future implementation: process the PDF file here

	const data = new FormData();
	data.append("file", file);
	const response = await fetch("/api/upload", {
		method: "POST",
		body: data,
	});

	console.log("Server response:", await response.json());
};

function App() {
	return (
		<div className="container">
			<Header title="Conversion Course" />
			<section className="hero">
				<p>Convert any PDF document into a set of question cards!</p>
			</section>
			<input
				type="file"
				accept="application/pdf"
				ref={fileInputRef}
				style={{ display: "none" }}
				onChange={handleFileChange}
			/>
			<Button
				text="Upload PDF"
				color="primary"
				handleClick={handleUploadButton}
			/>
		</div>
	);
}

export default App;
