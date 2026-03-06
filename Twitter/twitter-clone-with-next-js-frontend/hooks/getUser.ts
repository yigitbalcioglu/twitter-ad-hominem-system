import { getApiBaseUrl } from "@/lib/api";

export default async function GetUser(ownersId: string): Promise<IUserProps | null> {
    try {
        const response = await fetch(`${getApiBaseUrl()}/auth/users/${ownersId}/`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            return null;
        }

        const data = (await response.json()) as IUserProps;
        return data;
    } catch (error) {
        return null;
    }
}