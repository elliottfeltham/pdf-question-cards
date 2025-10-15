import "./styles/App.css";
import type { Question } from "./types";
import React from "react";
import Header from "./components/Header";
import CardContainer from "./components/CardContainer";
import FileUpload from "./components/FileUpload";

function App() {
	const [error, setError] = React.useState<string | null>(null);
	const [questions, setQuestions] = React.useState<Question[]>([]);

	return (
		<div className="container">
			<Header title="Conversion Course" />
			<FileUpload setQuestions={setQuestions} setError={setError} />
			{error ? (
				<p className="error">{error}</p>
			) : (
				<CardContainer questions={questions} />
			)}
		</div>
	);
}

export default App;
