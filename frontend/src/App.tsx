import "./styles/App.css";
import type { Question } from "./types";
import React from "react";
import Header from "./components/Header";
import CardContainer from "./components/CardContainer";
import FileUpload from "./components/FileUpload";
import Spinner from "./components/Spinner";

function App() {
	const [error, setError] = React.useState<string | null>(null);
	const [questions, setQuestions] = React.useState<Question[]>([]);
	const [loading, setLoading] = React.useState<boolean>(false);

	return (
		<div className="container">
			<Header title="Conversion Course" />
			<FileUpload
				setQuestions={setQuestions}
				setError={setError}
				setLoading={setLoading}
			/>
			{loading && (
				<div>
					<Spinner />
				</div>
			)}
			{error ? (
				<p className="error">{error}</p>
			) : (
				<CardContainer questions={questions} />
			)}
		</div>
	);
}

export default App;
