import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api, { getErrorMessage } from '@/lib/api';
import { useNotificationStore } from '@/lib/notifications';
import { API_ROUTES, CACHE_TIMES } from '@/lib/constants';
import { SkillStatus, SkillSource } from '@/types';
import type { SkillGraph, SkillNode } from '@/types';
import type { ApiResponse, AddSkillRequest } from '@/types/api';

export function useSkillGraph() {
  const queryClient = useQueryClient();
  const { addNotification } = useNotificationStore();

  // Fetch Skill Graph
  const skillGraphQuery = useQuery({
    queryKey: ['skills'],
    queryFn: async () => {
      const response = await api.get<ApiResponse<SkillGraph>>(
        API_ROUTES.SKILLS
      );
      return response.data.data!;
    },
    staleTime: CACHE_TIMES.SKILLS,
  });

  // Add Skill
  const addSkillMutation = useMutation({
    mutationFn: async (data: AddSkillRequest) => {
      const response = await api.post<ApiResponse<SkillNode>>(
        API_ROUTES.SKILLS,
        data
      );
      return response.data.data!;
    },
    onSuccess: (newSkill) => {
      // Optimistic update
      queryClient.setQueryData(['skills'], (old: SkillGraph | undefined) => {
        if (!old) return old;
        return {
          ...old,
          skills: [...old.skills, newSkill],
          totalSkills: old.totalSkills + 1,
        };
      });
      addNotification('success', 'Skill added successfully');
    },
    onError: (error) => {
      addNotification('error', getErrorMessage(error));
    },
  });

  return {
    skillGraph: skillGraphQuery.data,
    skills: skillGraphQuery.data?.skills || [],
    totalSkills: skillGraphQuery.data?.totalSkills || 0,
    verifiedSkills: skillGraphQuery.data?.verifiedSkills || 0,
    isLoading: skillGraphQuery.isLoading,
    isError: skillGraphQuery.isError,
    error: skillGraphQuery.error,
    addSkill: addSkillMutation.mutate,
    isAddingSkill: addSkillMutation.isPending,
  };
}
