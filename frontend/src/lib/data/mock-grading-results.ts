import type { BatchGradingResponse } from '$lib/types/grading';

export const mockGradingResults: BatchGradingResponse = {
	results: [
		{
			name: 'John Doe',
			overall_feedback:
				'Great job on the assignment! Your thesis was clear and your evidence was strong. Keep up the good work!',
			criteria_feedback: [
				{
					criteria_title: 'Thesis Statement',
					score: 7.5,
					score_max: 8,
					feedback:
						'Your thesis statement is clear and well-defined. It sets a strong foundation for your assignment.'
				},
				{
					criteria_title: 'Evidence and Support',
					score: 14,
					score_max: 20,
					feedback:
						'You provided some good examples, but consider adding more specific citations to strengthen your arguments.'
				},
				{
					criteria_title: 'Organization',
					score: 9,
					score_max: 10,
					feedback:
						'Your essay flows logically from introduction to conclusion. Great use of transitions!'
				}
			]
		},
		{
			name: 'Jane Smith',
			overall_feedback:
				'Good effort! Your writing shows promise, but there are areas that need improvement, particularly in thesis clarity and evidence support.',
			criteria_feedback: [
				{
					criteria_title: 'Thesis Statement',
					score: 5,
					score_max: 8,
					feedback: 'Your thesis is a bit vague. Try to be more specific about your main argument.'
				},
				{
					criteria_title: 'Evidence and Support',
					score: 10,
					score_max: 20,
					feedback:
						'You need more specific examples to support your points. Consider adding more quotations from the text.'
				},
				{
					criteria_title: 'Organization',
					score: 8,
					score_max: 10,
					feedback:
						'Good structure overall, but your body paragraphs could use clearer topic sentences.'
				}
			]
		},
		{
			name: 'Alex Johnson',
			overall_feedback:
				'Excellent work! This is one of the best essays in the class. Your analysis is thorough and well-presented.',
			criteria_feedback: [
				{
					criteria_title: 'Thesis Statement',
					score: 8,
					score_max: 8,
					feedback: 'Your thesis is compelling and precisely worded. Excellent job!'
				},
				{
					criteria_title: 'Evidence and Support',
					score: 19,
					score_max: 20,
					feedback:
						'Outstanding use of evidence. Every claim is well-supported with specific examples.'
				},
				{
					criteria_title: 'Organization',
					score: 10,
					score_max: 10,
					feedback:
						'Perfect organization. Your arguments build logically and your conclusion is strong.'
				}
			]
		}
	],
	total: 3
};
