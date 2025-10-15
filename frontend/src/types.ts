export type Question = {
    id: string;
    type: "theory" | "coding";
    prompt_md: string;
    solution_md?: string;
    solution_code?: string;
};