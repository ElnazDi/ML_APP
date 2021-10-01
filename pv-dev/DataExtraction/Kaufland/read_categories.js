() => {
    const categories = []
    const webpageCategoryList = [...document.querySelectorAll('.m-accordion__item--level-3')];
    categories = webpageCategoryList.filter(webpageCategory => {
        console.log(webpageCategory)
        const linkChild = webpageCategory.children[0];
        const category = {
            link: linkChild['href'],
            text: linkChild['innerText']
        }
        return category
    })
    console.log(categories);
    return categories
}