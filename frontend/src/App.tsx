import "./styles/App.css";
import type { Question } from "./types";
import React from "react";
import Header from "./components/Header";
import Button from "./components/Button";
import CardContainer from "./components/CardContainer";

const fileInputRef = React.createRef<HTMLInputElement>();

const handleUploadButton = () => {
	fileInputRef.current?.click();
};

function App() {
	const [questions, setQuestions] = React.useState<Question[]>([]);

	const handleFileChange = async (
		event: React.ChangeEvent<HTMLInputElement>
	) => {
		const file = event.target.files?.[0];
		if (!file) {
			console.log("No file selected");
			return;
		}
		console.log("Selected file:", file);

		const data = new FormData();
		data.append("file", file);
		const response = await fetch("/api/generate_questions", {
			method: "POST",
			body: data,
		});

		const responseData = await response.json();

		console.log("Server response:", responseData);

		setQuestions(responseData.raw.items);
	};

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
			<CardContainer questions={questions} />
		</div>
	);
}

export default App;
