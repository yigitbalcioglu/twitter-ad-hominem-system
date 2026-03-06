import { getApiBaseUrl } from "@/lib/api";

interface OwnerIdProp {
    ownersId: string;
}

export default async function GetCurrentUser({ ownersId }: OwnerIdProp) {
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