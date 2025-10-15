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

	onClick: () => void;
};

const Button = ({ text, color, onClick }: ButtonProps) => {
	return (
		<button
			className={`${styles.button} ${styles[color]}`}
			onClick={onClick}
		>
			<Upload className={styles.icon} />
			{text}
		</button>
	);
};

export default Button;
