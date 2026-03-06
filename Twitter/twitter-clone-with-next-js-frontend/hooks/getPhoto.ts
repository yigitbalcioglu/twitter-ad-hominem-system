import { getApiBaseUrl } from "@/lib/api";

const getPhoto = async (userId: string): Promise<string> => {
    try {
        const response = await fetch(`${getApiBaseUrl()}/auth/users/${userId}/`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            return "";
        }

        const data = (await response.json()) as IUserProps;
        return data.avatar ?? "";
    } catch (error) {
        return "";
    }
};

export default getPhoto;

