import styles from "./Button.module.css";
import { Upload } from "lucide-react";

type ButtonProps = {
	text: string;
	color:
		| "primary"
		| "blue"
		| "green"
		| "pink"
		| "yellow"
		| "purple"
		| "orange";

	handleClick: () => void;
};

const Button = ({ text, color, handleClick }: ButtonProps) => {
	return (
		<button
			className={`${styles.button} ${styles[color]}`}
			onClick={handleClick}
		>
			<Upload className={styles.icon} />
			{text}
		</button>
	);
};

export default Button;
