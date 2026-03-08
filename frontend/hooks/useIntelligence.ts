import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '@/lib/auth';
import api from '@/lib/api';

export function useSkillPriorities(limit = 5) {
  const { user } = useAuthStore();

  return useQuery({
    queryKey: ['skill-priorities', user?.userId, limit],
    queryFn: async () => {
      if (!user?.userId) return null;

      const response = await api.get(
        `/api/v1/intelligence/skill-priorities/${user.userId}?limit=${limit}`
      );
      return response.data.data;
    },
    enabled: !!user?.userId,
    staleTime: 5 * 60 * 1000,
  });
}
