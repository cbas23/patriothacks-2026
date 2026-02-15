import { z } from 'zod';

export const CriteriaFeedbackSchema = z.object({
	criteria_title: z.string(),
	score: z.number(),
	score_max: z.number(),
	feedback: z.string()
});

export type CriteriaFeedback = z.infer<typeof CriteriaFeedbackSchema>;

export const GradingResultSchema = z.object({
	name: z.string(),
	overall_feedback: z.string(),
	criteria_feedback: z.array(CriteriaFeedbackSchema),
	images: z.array(z.string()).optional(),
	ai_detection: z
		.object({
			is_ai_generated: z.boolean(),
			confidence: z.number()
		})
		.optional()
});

export type GradingResult = z.infer<typeof GradingResultSchema>;

export const BatchGradingResponseSchema = z.object({
	results: z.array(GradingResultSchema),
	total: z.number()
});

export type BatchGradingResponse = z.infer<typeof BatchGradingResponseSchema>;
