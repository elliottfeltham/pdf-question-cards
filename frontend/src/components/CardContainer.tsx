import QuestionCard from "./QuestionCard";

type CardContainerProps = {
	questions: string;
};
const CardContainer = ({ questions }: CardContainerProps) => {
	return (
		<div className="card-container">
			<QuestionCard question={questions} />
		</div>
	);
};

export default CardContainer;
