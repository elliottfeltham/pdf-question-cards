import "./styles/App.css";
import type { Question } from "./types";
import React from "react";
import Header from "./components/Header";
import CardContainer from "./components/CardContainer";
import FileUpload from "./components/FileUpload";
import Spinner from "./components/Spinner";
import { exportNotebook } from "./lib/api";

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
			{!error && questions.length > 0 ? (
				<>
					<CardContainer questions={questions} />
					<button
						style={{ margin: "2rem" }}
						onClick={() =>
							exportNotebook("Lecture Notebook", questions)
						}
						disabled={!questions.length}
					>
						Export Notebook (.ipynb)
					</button>
				</>
			) : (
				<p className="error">{error}</p>
			)}
		</div>
	);
}

export default App;
