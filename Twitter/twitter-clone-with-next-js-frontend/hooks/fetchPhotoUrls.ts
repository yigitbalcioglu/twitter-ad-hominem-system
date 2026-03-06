import getPhoto from "./getPhoto";

export default async function fetchRelatedUrls(
    users: IUserProps[] | null | undefined,
): Promise<IUserPhotoProps[]> {
    if (!users || users.length === 0) {
        return [];
    }

    try {
        const photoUrls: IUserPhotoProps[] = [];

        for (const user of users) {
            photoUrls.push({
                photoUrl: user.avatar ?? (await getPhoto(user.id)),
                userId: user.id,
            });
        }

        return photoUrls;
    } catch (error) {
        throw error;
    }
}
