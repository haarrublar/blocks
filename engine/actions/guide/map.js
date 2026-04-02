export const map = {
    ss: {
        ss_first_block: { x: 3, y: -60, z: -51 },
        ss_second_block: { x: 24, y: -60, z: -16 },
        detail: "Study Space",
    },
    gp: {
        gp_first_block: { x: 21, y: -60, z: -51 },
        gp_second_block: { x: 21, y: -60, z: -29 },
        detail: "Government Publications"
    },
};

export const mapBuildingsAreas = Object.values(map).flatMap(
    obj => Object.keys(obj).filter(key => key !== 'detail')
);