export type Question = {
    type: "theory" | "coding";
    prompt_md: string;
    solution_md?: string;
    starter_code?: string;
    solution_code?: string;
};