import QuestionCard from "./QuestionCard";
import type { Question } from "../types";

type CardContainerProps = {
	questions: Question[];
};

const colors = ["blue", "pink", "yellow", "purple", "orange"];

const CardContainer = ({ questions }: CardContainerProps) => {
	return (
		<div className="card-container">
			{questions.map((question, index) => {
				return (
					<QuestionCard
						key={question.id}
						question={question}
						color={colors[index % colors.length]}
						questionNumber={index + 1}
					/>
				);
			})}
		</div>
	);
};

export default CardContainer;
