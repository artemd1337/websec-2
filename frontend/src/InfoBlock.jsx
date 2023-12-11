function InfoBlock({objectName, objectProperties}) {
    return (
        <div className="info_block">
        <div className="object_name_block">
            <h2 className="object_name_string">{objectName}</h2>
            {objectProperties && objectProperties.map(property => (
                <p key={property} className="object_info_block">{property}</p>
            ))}
        </div>
    </div>
    );
}

export default InfoBlock;